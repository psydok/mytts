<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class CreateTableRating extends AbstractMigration
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
        $this->table('rating')
            ->addColumn('models_id', 'integer')
            ->addColumn('avg_rate', 'decimal')
            ->addColumn('avg_speed', 'decimal')
            ->addColumn('avg_len_text', 'decimal')
            ->addColumn('count_rate', 'integer')
            ->addIndex(['models_id'], ['unique' => true])
            ->addForeignKey('models_id', 'models', 'id',
                ['delete' => 'NO_ACTION', 'update' => 'NO_ACTION'])
            ->create();

        $this->table('rating')
            ->insert([
                [
                    'models_id' => 1,// 'fast_speech2'
                    'avg_rate' => 0.0,
                    'avg_speed' => 0.0,
                    'avg_len_text' => 0.0,
                    'count_rate' => 0.0,
                ],
                [
                    'models_id' => 2, //'forward_tacotron'
                    'avg_rate' => 0.0,
                    'avg_speed' => 0.0,
                    'avg_len_text' => 0.0,
                    'count_rate' => 0.0,
                ]
            ])
            ->save();
    }
}
