let editors = document.querySelectorAll(".block-editor");

editors.forEach((elem) => {
  const editor = CodeMirror.fromTextArea(elem.querySelector("textarea"), {
    mode: {
      name: "python",
      version: 3,
      singleLineStringErrors: false,
    },
    theme: "dracula",
    lineNumbers: true,
    indentUnit: 4,
    matchBrackets: true,
  });
  
  editor.setValue(
    "a = int(input())\nb = int(input())\nc = int(input())\nprint(a + b + c)"
  );
  
  async function main() {
    let pyodide = await loadPyodide({});
    return pyodide;
  }
  
  let pyodideReadyPromise = main();
  
  async function evaluatePython() {
    let pyodide = await pyodideReadyPromise;
  
    try {
      pyodide.runPython(`
      import io
      import sys
      sys.stdout = io.StringIO()
    `);
      pyodide.setStdin({stdin: () => {return '1\n2\n3'}});
      let result = await pyodide.runPython(editor.getValue());
      let stdout = await pyodide.runPython("sys.stdout.getvalue()");
      console.log(stdout);
    } catch (err) {
      console.log(err);
    }
  }

  let confirmButton = elem.querySelector("button");
  confirmButton.addEventListener("click", evaluatePython);

});