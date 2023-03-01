
import {ExecInput, ExecResult} from "./models";

/**
 * @klotho::execution_unit {
 *   id = "task-2"
 * }
 */
export function invokeCrossExec(input: ExecInput): ExecResult {
    return {id: input.id, status: 200, message: "ok"}
}