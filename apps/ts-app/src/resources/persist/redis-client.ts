import { createClient } from 'redis';

/**
 * @klotho::persist {
 *   id = "redis-client"
 * }
 */
export const redisClient = createClient();

export const redisClientConnected = redisClient.connect();