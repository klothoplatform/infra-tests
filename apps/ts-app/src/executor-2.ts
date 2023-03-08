import express = require("express");
import {testGetEmbeddedAsset, testListEmbeddedAssets} from "./tests/embed-assets-tests";
import {
    testGetRedisClusterEntry,
    testGetRedisEntry,
    testSetRedisClusterEntry,
    testSetRedisEntry
} from "./tests/persist/redis-tests";

/**
 * @klotho::execution_unit {
 *   id = "executor-2"
 * }
 */

// TODO: remove this separator after klotho-history/#321 is implemented
const separator = undefined;
// @klotho::embed_assets {
//  id = "embedded-assets"
//  include = ["/embedded-assets/**/*.txt"]
//  exclude = ["**/excluded-text.txt"]
// }


export const router2 = express.Router();

router2.get("/test/persist-redis/redis-get-entry", testGetRedisEntry);
router2.post("/test/persist-redis/redis-set-entry", testSetRedisEntry);
router2.get("/test/persist-redis/redis-cluster-get-entry", testGetRedisClusterEntry);
router2.post("/test/persist-redis/redis-cluster-set-entry", testSetRedisClusterEntry);

router2.get("/test/embed-assets/get-asset", testGetEmbeddedAsset);
router2.get("/test/embed-assets/list-assets", testListEmbeddedAssets);
