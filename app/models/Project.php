<?php
use Illuminate\Database\Eloquent\SoftDeletingTrait;

class Project extends Eloquent {

    use SoftDeletingTrait;

    protected $dates = ['deleted_at'];

	protected $table = 'projects';
}