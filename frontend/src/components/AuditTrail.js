import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Button, Spinner, Badge } from 'react-bootstrap';
import { complianceAPI } from '../services/api';

const AuditTrail = () => {
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAuditTrail();
  }, []);

  const fetchAuditTrail = async () => {
    try {
      const response = await complianceAPI.getAuditTrail(50);
      setAuditLogs(response.data.entries);
    } catch (err) {
      setError('Failed to fetch audit trail');
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const renderDetails = (details) => {
    if (!details) return 'No details';
    
    try {
      const parsedDetails = typeof details === 'string' ? JSON.parse(details) : details;
      
      if (typeof parsedDetails === 'object') {
        return (
          <div>
            {Object.entries(parsedDetails).map(([key, value]) => (
              <div key={key}>
                <strong>{key}:</strong> {JSON.stringify(value)}
              </div>
            ))}
          </div>
        );
      }
      
      return String(parsedDetails);
    } catch (e) {
      return String(details);
    }
  };

  if (loading) {
    return (
      <Container className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </Container>
    );
  }

  return (
    <Container>
      <Row className="mb-4">
        <Col>
          <h2>Audit Trail</h2>
          <p className="text-muted">System activity and user actions log</p>
        </Col>
      </Row>

      <Row>
        <Col>
          <Card className="dashboard-card">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <h5>Recent Activities</h5>
              <Button variant="outline-primary" size="sm" onClick={fetchAuditTrail}>
                Refresh
              </Button>
            </Card.Header>
            <Card.Body>
              {error && (
                <div className="alert alert-danger">{error}</div>
              )}
              
              <Table striped responsive>
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>User</th>
                    <th>Action</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLogs.map((log, index) => (
                    <tr key={index}>
                      <td>{formatTimestamp(log.timestamp)}</td>
                      <td>{log.username || 'System'}</td>
                      <td>
                        <Badge bg="info" className="text-capitalize">
                          {log.action_type}
                        </Badge>
                      </td>
                      <td>
                        <small className="text-muted">
                          {renderDetails(log.details)}
                        </small>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
              
              {auditLogs.length === 0 && (
                <div className="text-center text-muted py-4">
                  No audit logs found
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default AuditTrail;