<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class InsertSilero extends AbstractMigration
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
            ->insert([
                [
                    'generator' => 'silero',
                    'vocoder' => 'waveglow'
                ]
            ])
            ->save();

        $this->table('rating')
            ->insert([
                [
                    'models_id' => 3, //'silero'
                    'avg_rate' => 0.0,
                    'avg_speed' => 0.0,
                    'avg_len_text' => 0.0,
                    'count_rate' => 0.0,
                ]])
            ->save();
    }
}
