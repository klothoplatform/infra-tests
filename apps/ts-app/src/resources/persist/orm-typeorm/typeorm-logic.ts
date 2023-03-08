import "reflect-metadata"
import {DataSource} from "typeorm"
import {KV} from "./typeorm-model"


export const initialize = async (): Promise<DataSource> => {

    /** @klotho::persist  {
     *   id = "typeormDB"
     * }
     */
    const AppDataSource = new DataSource({
     type: "sqlite",
     database: ":memory:",
     entities: [KV],
     synchronize: true,
     logging: false,
   })
    
    // to initialize initial connection with the database, register all entities
    // and "synchronize" database schema, call "initialize()" method of a newly created database
    // once in your application bootstrap
    await AppDataSource.initialize()

    return AppDataSource
}

const dataSource: Promise<DataSource> = initialize();

export const set = async (key: string, value: string) => {
    const entry = new KV()
    entry.key = key
    entry.value = value
    await dataSource;
    await KV.save(entry)
}

export async function get (key: string): Promise<KV | null> {
    await dataSource;
    return (await KV.findOneBy({
        key: key,
    }));
}
