<!-- Extracted verbatim from searchtool/khan/vc-karaka/gemini_json.js lines 90–97 (exported as JSON_PROMPT_RULES). The prompt is built in code: ${…} / + v.x + / joined arrays mark where the input (verse, words, notes) is inserted at run time. -->

```js
const PROMPT_RULES = [
  '## JSON OUTPUT RULES (obey exactly)',
  '- Output ONLY the JSON value — no code fences, no prose before or after. It must parse with JSON.parse.',
  '- Put NO raw double-quote (") inside any string value. For a quotation inside Sanskrit text use guillemets ‹ ›;',
  '  in English fields use single quotes \'…\'. (A raw " inside a value is the #1 cause of invalid JSON.)',
  '- Put NO literal newline/tab inside a string value — keep each string on one line.',
  '- Balance every { } and [ ]. No trailing comma before } or ].',
].join('\n');
```
