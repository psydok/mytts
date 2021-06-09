<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class CreateTableModel extends AbstractMigration
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
        $this->table('models')
            ->addColumn('generator', 'string')
            ->addColumn('vocoder', 'string', ['default' => 'griffinlim'])
            ->addIndex(['generator', 'vocoder'], ['unique' => true])
            ->create();

        $this->table('models')
            ->insert([
                [
                    'generator' => 'fast_speech2'
                ],
                [
                    'generator' => 'forward_tacotron'
                ]
            ])
            ->save();
    }
}
