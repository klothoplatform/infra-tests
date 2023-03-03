
/**
 * @klotho::persist {
 *   id = "kv-map-dynamodb"
 * }
 */
const kvMap = new Map<string, any>();

export async function get(key: string): Promise<any> {
  return await kvMap.get(key);
}

export async function set(key: string, value: any): Promise<Map<string, any>> {
  return await kvMap.set(key, value);
}

export async function deleteElement(element: string): Promise<boolean> {
  return await kvMap.delete(element);
}

export async function clear() {
  await kvMap.clear();
}

export async function entries(): Promise<IterableIterator<[string, any]>> {
  return await kvMap.entries();
}

export async function has(element: string): Promise<boolean> {
  return await kvMap.has(element);
}

export {deleteElement as delete}
