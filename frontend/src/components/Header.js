import React from 'react';
import { Navbar, Nav, Button, Container } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Header = ({ user, onLogout }) => {
  const navigate = useNavigate();

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
      <Container>
        <Navbar.Brand href="#!" onClick={() => handleNavigation('/dashboard')} style={{ cursor: 'pointer' }}>
          📊 BrokerMint Compliance
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Nav className="me-auto">
            <Nav.Link href="#!" onClick={() => handleNavigation('/dashboard')}>Dashboard</Nav.Link>
            <Nav.Link href="#!" onClick={() => handleNavigation('/anomalies')}>Anomaly Detection</Nav.Link>
            <Nav.Link href="#!" onClick={() => handleNavigation('/ekyc')}>eKYC Verification</Nav.Link>
            <Nav.Link href="#!" onClick={() => handleNavigation('/reports')}>Reports</Nav.Link>
            <Nav.Link href="#!" onClick={() => handleNavigation('/audit')}>Audit Trail</Nav.Link>
          </Nav>
          <Navbar.Text className="me-3">
            Welcome, <strong>{user?.username}</strong> ({user?.role})
          </Navbar.Text>
          <Button variant="outline-light" size="sm" onClick={onLogout}>
            Logout
          </Button>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;