#!/usr/bin/env node
'use strict';

// Anonymous capture of the real GitHub DOM. No source-to-render comparison is
// performed here: the files contain observations for subsequent review.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {execFileSync} = require('node:child_process');
const {chromium} = require('playwright');

const git = (...args) => execFileSync('git', args, {maxBuffer:32*1024*1024});
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const repository = process.env.GITHUB_REPOSITORY;
const revision = git('rev-parse', 'HEAD').toString().trim();
if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repository || ''))
  throw new Error('Set GITHUB_REPOSITORY to the public owner/name');
if (!/^[0-9a-f]{40}$/.test(revision)) throw new Error('HEAD must be a full commit');
const files = git('ls-tree','-r','--name-only','-z',revision).toString().split('\0')
  .filter(file => /\.(md|markdown)$/i.test(file));
if (!files.length) throw new Error('No tracked Markdown pages');
const output = path.resolve('verification/output/hosted');
fs.mkdirSync(output, {recursive:true});
const tree = git('rev-parse', 'HEAD^{tree}').toString().trim();

function readMathematics() {
  const article = document.querySelector('article.markdown-body');
  const wrappers = [...article.querySelectorAll('math-renderer')];
  const hosts = wrappers.length ? wrappers : [...article.querySelectorAll('math')]
    .filter(node => !node.parentElement.closest('math,annotation,annotation-xml'));
  const math = hosts.map((host, index) => {
    const nodes = host.localName === 'math' ? [host] : [...host.querySelectorAll('math')]
      .filter(node => !node.parentElement.closest('math,annotation,annotation-xml'));
    const node = nodes[0];
    const tokens = node ? [...node.querySelectorAll('mi,mn,mo,mtext,ms')]
      .map(token => token.getBoundingClientRect()).filter(box => box.width && box.height) : [];
    let geometry = {measurable:false, available_width:article.clientWidth};
    if (tokens.length) {
      const left = Math.min(...tokens.map(box => box.left));
      const right = Math.max(...tokens.map(box => box.right));
      const top = Math.min(...tokens.map(box => box.top));
      const bottom = Math.max(...tokens.map(box => box.bottom));
      const width = right-left, height = bottom-top;
      geometry = {measurable:true, left, right, top, bottom, width, height,
        available_width:article.clientWidth, host_width:host.getBoundingClientRect().width,
        overflow:width > article.clientWidth+4, collapsed:height > 200 && height > 3*width};
    }
    return {index, host_tag:host.localName, in_table:!!host.closest('td,th'),
      mathml_count:nodes.length, mathml:node ? node.outerHTML : null,
      all_mathml:nodes.map(item => item.outerHTML), text:node ? node.textContent : '',
      geometry, errors:nodes.length === 1 ? [] : ['Expected one MathML representation']};
  });
  const errors = [...article.querySelectorAll('merror,[data-mjx-error],.katex-error')]
    .map(node => node.textContent.trim());
  return {math, errors, math_renderer_count:wrappers.length};
}

async function main() {
  const browser = await chromium.launch({headless:true});
  try {
    for (const width of [1440,760]) {
      const directory = path.join(output,String(width));
      fs.mkdirSync(directory,{recursive:true});
      const capture = {schema_version:1, capture_kind:'raw_anonymous_github_dom',
        repository, revision, tree, viewport:{width,height:1000},
        captured_at_utc:new Date().toISOString(),
        runtime:{node:process.version, playwright:require('playwright/package.json').version,
          browser:browser.version()}, capture_status:'incomplete', pages:[]};
      const context = await browser.newContext({viewport:{width,height:1000},deviceScaleFactor:1});
      try {
        for (const [index,file] of files.entries()) {
          const page = await context.newPage();
          const url = `https://github.com/${repository}/blob/${revision}/`+
            file.split('/').map(encodeURIComponent).join('/');
          const record = {path:file, revision, url, page_errors:[],
            source_sha256:hash(git('show',`${revision}:${file}`))};
          page.on('pageerror',error => record.page_errors.push(error.message));
          capture.pages.push(record);
          const stem = `${String(index+1).padStart(2,'0')}-${file.replace(/[^A-Za-z0-9_.-]/g,'_')}`;
          try {
            const response = await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
            record.response_status = response ? response.status() : null;
            record.observed_url = page.url();
            if (record.response_status !== 200) throw new Error(`HTTP ${record.response_status}`);
            if (new URL(record.observed_url).pathname !== new URL(url).pathname)
              throw new Error('Navigation left the pinned page');
            await page.locator('article.markdown-body').waitFor({state:'attached',timeout:30000});
            await page.waitForFunction(() => {
              const hosts = [...document.querySelectorAll('article.markdown-body math-renderer')];
              return hosts.every(host => !!host.querySelector('math'));
            },null,{timeout:30000});
            await page.evaluate(() => document.fonts.ready);
            Object.assign(record,await page.evaluate(readMathematics));
          } catch (error) {
            record.capture_error = String(error.message || error);
            throw error; // No retry or alternative route after an access/transport failure.
          } finally {
            const html = Buffer.from(await page.content());
            fs.writeFileSync(path.join(directory,stem+'.html'),html);
            record.html = {path:`${width}/${stem}.html`,sha256:hash(html),size_bytes:html.length};
            const screenshot = await page.screenshot({fullPage:true,timeout:60000});
            fs.writeFileSync(path.join(directory,stem+'.png'),screenshot);
            record.screenshot = {path:`${width}/${stem}.png`,sha256:hash(screenshot),size_bytes:screenshot.length};
            await page.close();
          }
        }
        capture.capture_status = 'complete';
      } finally {
        fs.writeFileSync(path.join(output,`raw-capture-${width}.json`),JSON.stringify(capture,null,2)+'\n');
        await context.close();
      }
    }
  } finally { await browser.close(); }
}

main().catch(error => {console.error(error.message || error);process.exitCode=1;});
