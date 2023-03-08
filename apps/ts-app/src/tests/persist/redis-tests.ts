import {redisClusterClient, redisClusterClientConnected} from "../../resources/persist/redis-cluster";
import {redisClient, redisClientConnected} from "../../resources/persist/redis-client";

export async function testGetRedisEntry(req, res) {
    await redisClientConnected;
    res.json(JSON.parse(await redisClient.get(req.query.key) || ""));
}

export async function testSetRedisEntry(req, res) {
    await redisClientConnected;
    await redisClient.set(req.body.key, JSON.stringify(req.body));
    res.send("success");
}

export async function testGetRedisClusterEntry(req, res) {
    await redisClusterClientConnected;
    res.json(JSON.parse(await redisClusterClient.get(req.query.key) || ""));
}

export async function testSetRedisClusterEntry(req, res) {
    await redisClusterClientConnected;
    await redisClusterClient.set(req.body.key, JSON.stringify(req.body));
    res.send("success");
}