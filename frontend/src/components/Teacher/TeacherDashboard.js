import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

function TeacherDashboard() {
  return (
    <Container className="mt-4">
      <Row>
        <Col>
          <h2>Teacher Dashboard</h2>
          <p>Welcome to the Teacher Panel</p>
        </Col>
      </Row>
      
      <Row className="mt-4">
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Create Exams</Card.Title>
              <Card.Text>
                Create and manage examinations
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>View Results</Card.Title>
              <Card.Text>
                Check student performance and results
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Question Bank</Card.Title>
              <Card.Text>
                Manage questions and question banks
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default TeacherDashboard;
