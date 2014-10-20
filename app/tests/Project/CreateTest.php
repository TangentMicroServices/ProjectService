<?php
class CreateTest extends TestCase {

	/* Create public repository, including wiki, issues and downloads [not in organization] */	
	public function testBasicPing()
	{
		$crawler = $this->client->request('POST', 'project');

		$this->assertTrue($this->client->getResponse()->isOk());
		$this->assertEquals($this->client->getResponse()->getContent(), json_encode(array('pong' => true)));
	}

}