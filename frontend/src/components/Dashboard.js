import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Alert, Badge, Table, Spinner } from 'react-bootstrap';
import { complianceAPI } from '../services/api';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await complianceAPI.getDashboard();
      setDashboardData(response.data);
    } catch (err) {
      setError('Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const getRiskBadge = (riskLevel) => {
    const variant = {
      'Low': 'success risk-low',
      'Medium': 'warning risk-medium',
      'High': 'danger risk-high',
      'Critical': 'danger risk-critical'
    }[riskLevel] || 'secondary';
    
    return <Badge className={variant}>{riskLevel}</Badge>;
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

  if (error) {
    return (
      <Container>
        <Alert variant="danger">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container>
      <Row className="mb-4">
        <Col>
          <h2>Compliance Dashboard</h2>
          <p className="text-muted">Real-time monitoring and analytics</p>
        </Col>
      </Row>

      {/* Statistics Cards */}
      <Row className="mb-4">
        <Col md={4}>
          <Card className="stat-card text-white text-center">
            <Card.Body>
              <h3>{dashboardData?.stats?.total_checks || 0}</h3>
              <p>Total Checks</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="stat-card text-white text-center">
            <Card.Body>
              <h3>{dashboardData?.stats?.anomalies_found || 0}</h3>
              <p>Anomalies Detected</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="stat-card text-white text-center">
            <Card.Body>
              <h3>{dashboardData?.stats?.high_risk_count || 0}</h3>
              <p>High Risk Items</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        {/* Alerts Section */}
        <Col md={6}>
          <Card className="dashboard-card">
            <Card.Header>
              <h5>Recent Alerts</h5>
            </Card.Header>
            <Card.Body>
              {dashboardData?.alerts?.map((alert, index) => (
                <Alert 
                  key={index} 
                  variant={alert.severity === 'high' ? 'danger' : 'warning'}
                  className="alert-item"
                >
                  <strong>{alert.title}</strong>
                  <br />
                  {alert.description}
                  <br />
                  <small>Due: {new Date(alert.deadline).toLocaleDateString()}</small>
                </Alert>
              ))}
            </Card.Body>
          </Card>
        </Col>

        {/* Anomalies Section */}
        <Col md={6}>
          <Card className="dashboard-card">
            <Card.Header>
              <h5>Recent Anomalies</h5>
            </Card.Header>
            <Card.Body>
              <Table striped responsive size="sm">
                <thead>
                  <tr>
                    <th>Ticker</th>
                    <th>Score</th>
                    <th>Risk</th>
                  </tr>
                </thead>
                <tbody>
                  {dashboardData?.anomalies?.map((anomaly, index) => (
                    <tr key={index}>
                      <td>{anomaly.ticker}</td>
                      <td>{anomaly.anomaly_score}</td>
                      <td>{getRiskBadge(anomaly.risk_level)}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;