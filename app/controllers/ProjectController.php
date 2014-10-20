<?php
class ProjectController extends BaseController {

	public function create()
	{
		$name = Input::get("name");
		$namePascalCase = str_replace(' ', '', ucwords($name));

		return Response::json(array('pong' => true));
	}

	private function _createGithubRepository($name, $description, $homepage, $private, $has_issues, $has_wiki, $has_downloads, $gitignore_template, $license_template, $auto_init)
	{
		$token = Config::get('graham-campbell/github::connections.main.token');

		$client = new Github\Client();
		$client->authenticate($token, 'http_token');
		$client->api('repos');
		
		$response = $client->getHttpClient()->post('user/repos', json_encode(array('name' => $name, 'description' => $description, 'homepage' => $homepage, 'private' => $private, 'has_issues' => $has_issues, 'has_wiki' => $has_wiki, 'has_downloads' => $has_downloads, 'gitignore_template' => $gitignore_template, 'license_template' => $license_template, 'auto_init' => $auto_init)));
		$repo     = Github\HttpClient\Message\ResponseMediator::getContent($response);	
	}	

}