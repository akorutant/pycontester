
const output = document.getElementById("output");


const editor = CodeMirror.fromTextArea(document.getElementById("code"), {
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
  "a = int(input())\nb = int(input())\nc = int(input())\nprint(a+b+c )"
);
output.value = "Initializing...\n";


function addToOutput(stdout) {
  output.value += ">>> " + "\n" + stdout + "\n";
}

async function main() {
  let pyodide = await loadPyodide({

  });
  output.value = pyodide.runPython(`
    import sys
    sys.version
  `);
  output.value += "\n" + "Python Ready !" + "\n";

  return pyodide;
}


let pyodideReadyPromise = main();

async function evaluatePython() {
  let pyodide = await pyodideReadyPromise;

  try {
    pyodide.runPython(`
		import io
		sys.stdout = io.StringIO()
	`);
    pyodide.setStdin({stdin: () => {return '1\n2\n3'}});
    let result = pyodide.runPython(editor.getValue());
    let stdout = pyodide.runPython("sys.stdout.getvalue()");
    console.log(stdout);
    addToOutput(stdout);
  } catch (err) {
    addToOutput(err);
  }
}
