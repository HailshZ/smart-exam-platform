import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

function AdminDashboard() {
  return (
    <Container className="mt-4">
      <Row>
        <Col>
          <h2>Admin Dashboard</h2>
          <p>Welcome to the Admin Panel</p>
        </Col>
      </Row>
      
      <Row className="mt-4">
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>User Management</Card.Title>
              <Card.Text>
                Manage students, teachers, and user approvals
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>System Overview</Card.Title>
              <Card.Text>
                View system statistics and performance
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Settings</Card.Title>
              <Card.Text>
                Configure platform settings and preferences
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default AdminDashboard;
