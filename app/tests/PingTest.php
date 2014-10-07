<?php

class PingTest extends TestCase {
	
	/**
	 * A basic functional ping test example.
	 *
	 * @return void
	 */

	public function testBasicPing()
	{
		$crawler = $this->client->request('GET', '/api/ping/');

		$this->assertTrue($this->client->getResponse()->isOk());
		$this->assertEquals($this->client->getResponse()->getContent(), json_encode(array('pong' => true)));
	}

}