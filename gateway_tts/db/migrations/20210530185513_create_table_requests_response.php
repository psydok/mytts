<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class CreateTableRequestsResponse extends AbstractMigration
{
    /**
     * Change Method.
     *
     * Write your reversible migrations using this method.
     *
     * More information on writing migrations is available here:
     * https://book.cakephp.org/phinx/0/en/migrations.html#the-change-method
     *
     * Remember to call "create()" or "update()" and NOT "save()" when working
     * with the Table class.
     */
    public function change(): void
    {
        $this->table('requests')
            ->addColumn('models_id', 'integer')
            ->addColumn('text', 'string')
            ->addColumn('created', 'timestamp',
                ['default' => 'CURRENT_TIMESTAMP'])
            ->addForeignKey('models_id', 'models', 'id',
                ['delete' => 'CASCADE', 'update' => 'NO_ACTION'])
            ->create();

        $this->table('responses')
            ->addColumn('requests_id', 'integer')
            ->addColumn('filename', 'string')
            ->addColumn('speed', 'decimal')
            ->addColumn('len_text', 'integer')
            ->addColumn('rate', 'integer', ['null' => true, 'default' => null])
            ->addIndex(['requests_id'], ['unique' => true])
            ->addForeignKey('requests_id', 'requests', 'id',
                ['delete' => 'CASCADE', 'update' => 'NO_ACTION'])
            ->create();
    }
}
