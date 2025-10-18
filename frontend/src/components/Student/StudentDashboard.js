import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

function StudentDashboard() {
  return (
    <Container className="mt-4">
      <Row>
        <Col>
          <h2>Student Dashboard</h2>
          <p>Welcome to your learning portal</p>
        </Col>
      </Row>
      
      <Row className="mt-4">
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Take Exams</Card.Title>
              <Card.Text>
                Access available examinations
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>View Results</Card.Title>
              <Card.Text>
                Check your exam results and progress
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Profile</Card.Title>
              <Card.Text>
                Manage your profile and settings
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default StudentDashboard;
