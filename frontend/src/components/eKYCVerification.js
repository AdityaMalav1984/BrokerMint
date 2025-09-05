import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Spinner } from 'react-bootstrap';
import { complianceAPI } from '../services/api';

const eKYCVerification = () => {
  const [formData, setFormData] = useState({
    document_type: 'aadhaar',
    document_data: { number: '' }
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  console.log('eKYC Component rendered'); // Debug log

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      console.log('Submitting:', formData); // Debug log
      const response = await complianceAPI.verifyIdentity(formData);
      console.log('Response:', response.data); // Debug log
      setResult(response.data);
    } catch (err) {
      console.error('Error:', err); // Debug log
      setError(err.response?.data?.error || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'document_number') {
      setFormData({
        ...formData,
        document_data: { number: value }
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  return (
    <Container>
      <Row className="mb-4">
        <Col>
          <h2>eKYC Verification</h2>
          <p className="text-muted">Electronic Know Your Customer verification</p>
        </Col>
      </Row>

      <Row>
        <Col md={6}>
          <Card className="dashboard-card">
            <Card.Header>
              <h5>Verify Identity</h5>
            </Card.Header>
            <Card.Body>
              {error && <Alert variant="danger">{error}</Alert>}
              
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Document Type</Form.Label>
                  <Form.Select
                    name="document_type"
                    value={formData.document_type}
                    onChange={handleInputChange}
                  >
                    <option value="aadhaar">Aadhaar Card</option>
                    <option value="pan">PAN Card</option>
                    <option value="passport">Passport</option>
                  </Form.Select>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Document Number</Form.Label>
                  <Form.Control
                    type="text"
                    name="document_number"
                    placeholder="Enter document number"
                    value={formData.document_data.number}
                    onChange={handleInputChange}
                  />
                </Form.Group>

                <Button 
                  variant="primary" 
                  type="submit"
                  disabled={loading}
                >
                  {loading ? <Spinner animation="border" size="sm" /> : 'Verify Identity'}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          {result && (
            <Card className="dashboard-card">
              <Card.Header>
                <h5>Verification Result</h5>
              </Card.Header>
              <Card.Body>
                <Alert variant={result.success ? 'success' : 'warning'}>
                  <strong>Status: {result.status}</strong>
                  <br />
                  {result.success ? (
                    <>
                      Verification Score: {(result.score * 100).toFixed(1)}%
                      <br />
                      <small>Verification ID: {result.verification_id}</small>
                    </>
                  ) : (
                    result.error
                  )}
                </Alert>
                
                {result.success && (
                  <div>
                    <h6>Next Steps:</h6>
                    <ul>
                      <li>Document verification completed</li>
                      <li>Compliance review scheduled</li>
                      <li>Results will be available in audit trail</li>
                    </ul>
                  </div>
                )}
              </Card.Body>
            </Card>
          )}

          <Card className="dashboard-card mt-4">
            <Card.Header>
              <h6>Supported Documents</h6>
            </Card.Header>
            <Card.Body>
              <ul>
                <li><strong>Aadhaar Card:</strong> 12-digit number</li>
                <li><strong>PAN Card:</strong> 10-character alphanumeric</li>
                <li><strong>Passport:</strong> 8-character alphanumeric</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default eKYCVerification;