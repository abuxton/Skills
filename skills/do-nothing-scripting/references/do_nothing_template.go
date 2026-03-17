// do_nothing_template.go
//
// TEMPLATE — Do-Nothing Script (Go implementation)
// Generated from: <source file or procedure description>
//
// A do-nothing script encodes a manual procedure as a sequence of steps.
// Each step prints instructions and waits for the operator to act. Steps
// that produce values (e.g. a generated filename, a retrieved ID) declare
// named outputs, which subsequent steps can reference as inputs.
//
// To automate a step: remove it from the donothing procedure and add the
// equivalent Go function call in main() before pcd.Execute(). The remaining
// steps in the procedure are untouched.
//
// Reference implementation: https://github.com/danslimmon/donothing
// Pattern: https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/
//
// Usage:
//   go run do_nothing_template.go           # run interactively
//   go run do_nothing_template.go --print   # print procedure as Markdown
//
// To use the donothing library in your own module:
//   go mod init example.com/your-procedure
//   go get github.com/danslimmon/donothing
// ------------------------------------------------------------------------------

package main

import (
	"fmt"
	"os"

	"github.com/danslimmon/donothing"
)

func procedure() *donothing.Procedure {
	pcd := donothing.NewProcedure()
	pcd.Short(`<Procedure Name>`)
	pcd.Long(`
		<Describe the procedure here. Markdown is supported.>

		Refer to any relevant documentation or runbooks below:
		- [Example Docs](https://example.com/docs)
	`)

	// --------------------------------------------------------------------------
	// Step 1 — Collect context
	// Declares a named output ("TargetName") that later steps can reference.
	// The operator will be prompted to provide the value at runtime.
	// When ready to automate: remove this step, compute the value in Go, and
	// pass it to the steps that need it.
	// --------------------------------------------------------------------------
	pcd.AddStep(func(step *donothing.Step) {
		step.Name("collectContext")
		step.Short("Collect the required context")
		step.OutputString(
			"TargetName",
			"The target you will be operating on (e.g. server name, environment, or ticket ID)",
		)
		step.Long(`
			Identify the target you will be operating on (e.g. a server name,
			environment name, or ticket ID) and enter it when prompted below.
		`)
	})

	// --------------------------------------------------------------------------
	// Step 2 — Manual step that consumes output from Step 1
	// InputString("TargetName", true) means this step requires the output named
	// "TargetName" from a previous step. The value will be shown in the step
	// instructions at runtime.
	// --------------------------------------------------------------------------
	pcd.AddStep(func(step *donothing.Step) {
		step.Name("verifyPrerequisites")
		step.Short("Verify prerequisites are met")
		step.InputString("TargetName", true)
		step.Long(`
			Check that the following are in place for @@TargetName@@:

			1. You have the necessary permissions.
			2. All dependencies are installed.
			3. No other operator is currently working on this target.
		`)
	})

	// --------------------------------------------------------------------------
	// Step 3 — Manual step that both consumes an input and produces an output
	// When this step is ready to automate, replace it with a Go function that
	// performs the action and returns the result, then remove this AddStep block.
	// --------------------------------------------------------------------------
	pcd.AddStep(func(step *donothing.Step) {
		step.Name("runMainTask")
		step.Short("Run the main task")
		step.InputString("TargetName", true)
		step.OutputString(
			"TaskResult",
			"The result or identifier produced by the main task",
		)
		step.Long(`
			Perform the main task against @@TargetName@@.

			Record the result or output identifier and enter it when prompted below.
		`)
	})

	// --------------------------------------------------------------------------
	// Step 4 — Verification step using the result from Step 3
	// --------------------------------------------------------------------------
	pcd.AddStep(func(step *donothing.Step) {
		step.Name("verifyOutcome")
		step.Short("Verify the outcome")
		step.InputString("TaskResult", true)
		step.Long(`
			Confirm that the task completed successfully:

			- Check the result: @@TaskResult@@
			- Open the relevant dashboard and verify the change is reflected.
			- If anything looks wrong, roll back before proceeding.
		`)
	})

	// --------------------------------------------------------------------------
	// Step 5 — Housekeeping (no inputs or outputs needed)
	// --------------------------------------------------------------------------
	pcd.AddStep(func(step *donothing.Step) {
		step.Name("cleanup")
		step.Short("Clean up and close out")
		step.Long(`
			1. Update the ticket or change record to mark this task as complete.
			2. Notify any stakeholders who need to know.
			3. Remove any temporary files or credentials you created.
		`)
	})

	return pcd
}

func main() {
	pcd := procedure()

	// Validate the procedure definition before running
	if problems, err := pcd.Check(); err != nil {
		fmt.Fprintf(os.Stderr, "Procedure definition has problems:\n")
		for _, p := range problems {
			fmt.Fprintf(os.Stderr, "  - %s\n", p)
		}
		os.Exit(1)
	}

	// Pass --print to generate Markdown documentation instead of running interactively
	if len(os.Args) > 1 && os.Args[1] == "--print" {
		if err := pcd.Render(os.Stdout); err != nil {
			fmt.Fprintf(os.Stderr, "Error rendering procedure: %v\n", err)
			os.Exit(1)
		}
		return
	}

	if err := pcd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Error executing procedure: %v\n", err)
		os.Exit(1)
	}
}
