import express = require("express");
import {testIsUsingCustomDockerfile} from "./tests/custom-dockerfile-tests";

/**
 * @klotho::execution_unit {
 *   id = "custom-dockerfile"
 * }
 */

export const router3 = express.Router();


router3.get("/test/exec/execute-custom-dockerfile", testIsUsingCustomDockerfile);
