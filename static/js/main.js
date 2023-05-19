let editors = document.querySelectorAll(".block-editor");

editors.forEach((task) => {
	const editor = CodeMirror.fromTextArea(task.querySelector("textarea"), {
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
	function main() {
		let pyodide = loadPyodide({});
		return pyodide;
	}
	let pyodideReadyPromise = main();
	async function evaluatePython() {
		let pyodide = await pyodideReadyPromise;
		try {
			let tests = task.querySelectorAll(".test-case>p");
			tests.forEach((test) => {

				pyodide.runPython(`
					import io
					import sys
					sys.stdout = io.StringIO()`);
				pyodide.setStdin({
					stdin: () => {
						return `${test.dataset.input}`;
					},
				});
				let out_test = test.dataset.output;
				let result = pyodide.runPython(editor.getValue());
				let stdout = pyodide.runPython("sys.stdout.getvalue()");
				if (stdout.trim() == out_test.trim()) {
					test.classList.add("circle-green");
				} else {
					test.classList.add("circle-red");
				}
			});
		} catch (err) {
			console.log(err);
		}
	}

	let confirmButton = task.querySelector("button");
	confirmButton.addEventListener("click", evaluatePython);
});
