# Code Weaver: The AI Patch Integration Tool

Have you ever asked an AI for code, and it gives you an abbreviated response like this?

```javascript
function myFunction() {
  // ... new logic here ...
}

// ... All other functions are unchanged ...
```

This is a huge pain. You're forced to manually copy and paste, risking errors and wasting time. **Code Weaver solves this problem.**

Code Weaver is a simple but powerful Python GUI application that acts as an intelligent "diff" tool. It takes your original master code file and a new "patch" file from an AI, and it intelligently weaves them together to produce a single, complete, and unabbreviated final script.

![Screenshot of Code Weaver App](URL_TO_YOUR_SCREENSHOT.png) 
*(You should take a screenshot of your app and upload it to the repo to replace this line)*

## The Problem It Solves

-   **AI Code Abbreviation:** AI assistants often abbreviate code for brevity, leaving you with the tedious task of manual integration.
-   **Risk of Manual Errors:** Manually copy-pasting functions is slow and highly prone to errors, like missing a function or pasting it in the wrong place.
-   **Lack of Versioning:** It's hard to track changes or revert to a previous version when you're just manually editing one file.

## How Code Weaver Works

Code Weaver provides a simple, visual interface to solve this problem permanently.

1.  **Load or Paste:** You can either visually select your `master` file and `patch` file using a file browser, or paste the code directly into two side-by-side text editors.
2.  **Integrate & Preview:** Click the "Integrate & Preview" button. Code Weaver reads both sources and:
    -   Identifies any functions in the patch marked with `/* Unchanged */`.
    -   Pulls the full, original body of those unchanged functions from your master code.
    -   Combines them with the new/updated functions from your patch.
    -   Displays the final, perfectly merged code in a "Result" panel for you to review.
3.  **Copy to Clipboard:** Click one button to copy the entire final script to your clipboard, ready to be pasted into your IDE or script editor.

## Features

-   **Language Agnostic:** Works with any language that uses `function` declaration and curly braces `{}`, like JavaScript, Google Apps Script, Java, C#, etc.
-   **Visual Interface:** No command line needed. A clean, modern GUI built with Python and ttkbootstrap.
-   **Dual Input Mode:** Choose to work with files on your computer or paste code directly into the app.
-   **Instant Preview:** See the result of the merge before you commit to it.
-.  **One-Click Copy:** Easily grab the final code.

## How to Use

### Prerequisites
- Python 3 installed on your machine.
- The `ttkbootstrap` library.

### Installation

1.  First, install the required library from your terminal:
    ```bash
    pip install ttkbootstrap
    ```
2.  Download the `code_weaver_app.py` file from this repository.

### Running the App

1.  Open your terminal or command prompt.
2.  Navigate to the directory where you saved the file.
3.  Run the application with the following command:
    ```bash
    python code_weaver_app.py
    ```

The Code Weaver window will appear, ready to help you streamline your development workflow!

---
*This tool was born from a real-world need to manage a complex Google Apps Script project. Special thanks to my co-developer, Thomas, for his brilliant ideas and rigorous testing.*
