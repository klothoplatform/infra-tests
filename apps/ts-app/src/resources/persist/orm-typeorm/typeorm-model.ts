import { Entity, PrimaryGeneratedColumn, Column, BaseEntity } from "typeorm"

@Entity("typeorm_db_users")
export class KV extends BaseEntity {

    @Column({primary: true})
    key: string

    @Column()
    value: string
}