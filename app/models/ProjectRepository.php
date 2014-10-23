<?php
use Illuminate\Database\Eloquent\SoftDeletingTrait;

class ProjectRepository extends Eloquent {

    use SoftDeletingTrait;

    protected $dates = ['deleted_at'];

	protected $table = 'project_repositories';

	public function project()
	{
		return $this->hasOne('Project');
	}

	public function repository_type()
	{
		return $this->hasOne('RepositoryType');
	}

}