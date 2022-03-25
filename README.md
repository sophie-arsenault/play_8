
Welcome to play_8! This is a flake8 extension meant to help you write unique selector strings for Playwright tests, so that you can avoid confusing errors and flaky tests.

*Although these warnings are inherently opinionated, play_8 is not meant to be configurable for the moment, as there are only a handful of checks. Please let us know if you have any suggestions for improvement.


Playwright supports many different selector engines, which is great for flexibility, but with it comes the opportunity to write selectors that depend too heavily on the exact structure of the web app you're testing.
Fragile selectors like these can create difficult-to-find bugs and behaviour without a lot of valid information to go from, and will require you to rewrite your selectors more often.

To ensure your tests are stable and follow best practices, this plugin will raise the following warnings when creating selector strings:


PLY801 = 'PLY801 `:has-text()` pseudo-class should have an html tag specified at the start.

:has-text will match any element containing the text specified, so it’s not an exact match. Therefore, if you don’t specify an element, it will select the first element anywhere in the DOM that might contain that text.
This warning is there to remind you to add a more specific element tag instead of invoking a bare :has-text, so you can be certain you're selecting the right element.

PLY802 = 'PLY802 string starting with `..` denotes use of x-path which is not allowed’

and

PLY803 = 'PLY803 string starting with `//` denotes use of x-path which is not allowed’

x-path treats the DOM as a giant xml document, so it relies entirely on page structure and can easily break with any changes to that structure.
This warning suggests using an alternative, less-location dependant method of selecting elements. See https://playwright.dev/docs/selectors#avoid-selectors-tied-to-implementation.

PLY804 = 'PLY804 use of `nth-child` is discouraged.’
            ’Select a more specific selector to avoid structural dependency issues.’

n-th child will select the nth element that is a child of the currently selected element. It depends entirely on page structure, which is inherently more fragile than creating a unique selector for an element. If someone creates a new child element or the list gets re-ordered, your selector will no longer point to the correct one without necessarily notifying you.


PLY805 = 'PLY805 use of more than one query operator `>>` may cause structural dependency issues.’

Querying a child element once is generally fine, but chaining queries makes your selector too dependent on page structure.