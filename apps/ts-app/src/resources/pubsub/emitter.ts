import * as events from "events"

/**
 * @klotho::pubsub {
 *   id = "pubsub-emitter"
 * }
 */
export const pubsubEmitter = new events.EventEmitter();