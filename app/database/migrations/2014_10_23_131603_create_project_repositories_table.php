<?php

use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateRepositoriesTable extends Migration {

	/**
	 * Run the migrations.
	 *
	 * @return void
	 */
	public function up()
	{
		Schema::create('project_repositories', function($table)
		{
		    $table->increments('id');
			$table->integer('project_id')->unsigned();
			$table->foreign('project_id')->references('id')->on('projects');
			$table->integer('repository_type_id')->unsigned();
			$table->foreign('repository_type_id')->references('id')->on('repository_types');
		    $table->string('homepage_url', 260)->nullable();
		    $table->boolean('has_wiki')->default(true);
		    $table->boolean('has_issues')->default(true);
		    $table->boolean('has_downloads')->default(true);
		    $table->timestamps();
		    $table->softDeletes();
		});
	}

	/**
	 * Reverse the migrations.
	 *
	 * @return void
	 */
	public function down()
	{
		Schema::drop("project_repositories");
	}

}
