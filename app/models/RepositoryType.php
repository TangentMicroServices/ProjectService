<?php
use Illuminate\Database\Eloquent\SoftDeletingTrait;

class RepositoryType extends Eloquent {

    use SoftDeletingTrait;

    protected $dates = ['deleted_at'];

	protected $table = 'repository_types';
}