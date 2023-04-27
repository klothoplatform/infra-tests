import {createCluster} from 'redis';

/**
 * @klotho:disabled::persist {
 *   id = "redis-cluster"
 * }
 */
export const redisClusterClient = createCluster({
    rootNodes:[
        {
            url: 'redis://127.0.0.1:8001'
        },
        {
            url: 'redis://127.0.0.1:8002'
        },
        {
            url: 'redis://127.0.0.1:8003'
        }
    ],
});

export const redisClusterClientConnected = redisClusterClient.connect();