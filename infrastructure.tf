provider "aws" {
  region = "eu-west-2"
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow inbound traffic on port 80 and 22"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "fastapi_instance" {
  ami           = "ami-04b9e92b5572fa0d3"  # Replace with the AMI ID for your region
  instance_type = "t2.micro"                # Change based on your needs
  key_name      = "your-key-pair"           # Replace with your EC2 key pair name
  security_groups = [aws_security_group.web_sg.name]

  tags = {
    Name = "FastAPIWeatherService"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y python3-pip
              sudo pip3 install fastapi uvicorn
              # Add commands to clone the repository and start the service
              git clone https://github.com/Parissai/fastapi-weather-service.git
              cd fastapi-weather-service
              pip3 install -r requirements.txt
              nohup uvicorn app.main:app --host 0.0.0.0 --port 80 --reload &
              EOF
}

output "instance_ip" {
  value = aws_instance.fastapi_instance.public_ip
}

resource "aws_db_instance" "mydb" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "13.2"
  instance_class       = "db.t2.micro"
  db_name              = "weatherdb"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.postgres13"
  skip_final_snapshot  = true
  publicly_accessible  = true

  tags = {
    Name = "MyDatabase"
  }
}

output "db_endpoint" {
  value = aws_db_instance.mydb.endpoint
}
