import React from 'react';
import { Container, Card, Alert } from 'react-bootstrap';

const Placeholder = ({ title }) => {
  return (
    <Container>
      <h2>{title}</h2>
      <Card>
        <Card.Body>
          <Alert variant="info">
            {title} component is working! This is a placeholder.
          </Alert>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Placeholder;