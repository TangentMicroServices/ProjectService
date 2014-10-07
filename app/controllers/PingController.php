<?php

class PingController extends BaseController {

	public function getPing()
	{
		return Response::json(array('pong' => true));
	}

}