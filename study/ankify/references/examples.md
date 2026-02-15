# ANKIFY Non-Normative Examples (v4)

These examples illustrate correct behavior. They do NOT introduce new rules.

## Example: Rule Application Plan

```
INPUT: "Auth Middleware" note (Pure Code, 2 code blocks, 1 distinction)

Tier 1 Rule Application Plan:
- PR-0003 (Generation Effect) -> APPLICABLE: Paraphrase all code explanations
- PR-0004 (Hidden Models) -> APPLICABLE: 1 MODEL card for auth flow
- PR-0005 (Behavior Change) -> APPLICABLE: 1 FAILURE MODE card ("What if you skip token verification?")
- PR-0017 (Idea Interaction) -> NOT APPLICABLE: No cross-concept comparisons
- PR-0038 (Counter-Evidence) -> NOT APPLICABLE: No contradictions
- PR-0045 (Negation) -> APPLICABLE: 1 distinction -> 1 NEGATION card
- PR-0047 (Mere-Exposure) -> APPLICABLE: Code cards use "Write..." format
- EL-PR-0003 (Basics-First) -> APPLICABLE: Theory cards before code cards
- EL-PR-0004 (Atomicity) -> APPLICABLE: Code blocks decomposed (>5 lines)
- Orphan Rule -> APPLICABLE: >=1 card per structural element per H2
- SDI Rule -> APPLICABLE: 6 structural elements -> target 6-15 cards (SDI 1.0-2.5)
- 10-min Rule -> APPLICABLE: Filter trivial boilerplate

Estimated cards: 10 (3 theory, 5 code, 1 negation, 1 failure mode)
```

## Example: Code Block Decomposition

Bad (monolithic, no context):

```
FRONT: Write the client-side script that fetches /weather and updates messages.
BACK: [20 lines of code]
```

Good (4 atomic cards):

```
Card 1 - DOM Selection:
FRONT: Given an HTML page with a <form>, <input>, and elements #message-1, #message-2,
       write the DOM query lines.
BACK:  const weatherForm = document.querySelector('form');
       const search = document.querySelector('input');
       const messageOne = document.querySelector('#message-1');
       const messageTwo = document.querySelector('#message-2');

Card 2 - Submit Handler:
FRONT: Given weatherForm and search elements, write the submit event listener
       that prevents default and sets messageOne to 'Loading...'.
BACK:  weatherForm.addEventListener('submit', (e) => {
         e.preventDefault();
         const location = search.value;
         messageOne.textContent = 'Loading...';
       });

Card 3 - Fetch + Display:
FRONT: Inside a submit handler, given location and messageOne/messageTwo,
       write the fetch call to /weather?address=... that displays the data.
BACK:  fetch('/weather?address=' + encodeURIComponent(location))
         .then(response => response.json())
         .then(data => {
           messageOne.textContent = data.location;
           messageTwo.textContent = data.weather_descriptions[0];
         });

Card 4 - Error Handling:
FRONT: Add .catch() to the fetch chain that sets messageOne to the error
       and clears messageTwo.
BACK:  .catch((error) => {
         messageOne.textContent = 'An error occurred: ' + error.message;
         messageTwo.textContent = '';
       });
```

## Example: Redundancy Handling

Bad (Duplicate questions for same code):
```tsv
# Card 1
<strong>JS: Array</strong><br>Write code to sort an array.	...
# Card 2
<strong>JS: Array</strong><br>How do you sort an array?	...
```

Good (Distinct variants):
```tsv
# Card 1 (Basic)
<strong>JS: Array</strong><br>Write code to sort an array of strings alphabetically.	...
# Card 2 (Comparator)
<strong>JS: Array</strong><br>Write code to sort an array of numbers in ascending order (fixing the default behavior).	...
```

## Example: Valid TSV Output

```tsv
<strong>JS: Closures</strong><br>Write a function that...\t<pre style='text-align:left; font-family:monospace;'><code>function x() {<br>&nbsp;&nbsp;let count = 0;<br>&nbsp;&nbsp;return function() { return ++count; };<br>}</code></pre>\tobsidian://open?vault=mohamed&file=javascript%2Fclosures
<strong>React: useEffect</strong><br>When does the cleanup run?\tIt runs on unmount AND before re-running the effect.\tobsidian://open?vault=mohamed&file=react%2Fhooks
```

## Example: Invalid TSV (Do Not Do This)

```tsv
# WRONG - Rule/Evidence in FRONT:
<strong>MongoDB</strong><br>How?<br><strong>Rule:</strong> TOPIC_active_recall\t...\tobsidian://...

# WRONG - Vault not 'mohamed':
...\tobsidian://open?vault=programming&file=...

# WRONG - Path not URL-encoded:
...\tobsidian://open?vault=mohamed&file=node/mosh/mongodb

# WRONG - REAL NEWLINES in code:
<strong>C++</strong><br>Write swap.\t<pre><code>void swap(int *a, int *b) {
    int temp = *a;  <- THIS BREAKS TSV
}</code></pre>\tobsidian://...
```
