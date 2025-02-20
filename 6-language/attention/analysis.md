# Analysis

## Layer 5, Head 7

This attention head seems to focus on pronoun resolution. Specifically, it helps resolve references to subjects earlier in the sentence. For example, in the sentence:

- "John went to the store because he needed milk."
  - The pronoun "he" strongly attends to "John," suggesting that this head identifies coreference resolution.
- "Sarah picked up the book and placed it on the table."
  - "It" attends to "book," demonstrating the same pattern.

## Layer 9, Head 3

This attention head appears to focus on verb-object relationships. It assigns strong attention from verbs to their corresponding objects. For example:

- "The cat chased the mouse."
  - The verb "chased" strongly attends to "mouse."
- "She quickly ate the delicious apple."
  - "Ate" attends to "apple," suggesting that this head captures direct object dependencies.
