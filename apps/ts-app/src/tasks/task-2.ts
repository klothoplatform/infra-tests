
import {ExecInput, ExecResult} from "./models";

/**
 * @klotho::execution_unit {
 *   id = "task-2"
 * }
 */
export async function invokeCrossExec(input: ExecInput): Promise<ExecResult> {
    return {id: input.id, status: 200, message: "ok"}
}