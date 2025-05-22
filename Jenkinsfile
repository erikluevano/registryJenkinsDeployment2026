pipeline {
    agent any
    environment {
        REGISTRY = 'registry.alex-mauricio.com.mx'
        IMAGE_NAME = 'cargas-academicas'
        VERSION = "v${BUILD_NUMBER}"
        USER_PROD = 'ubuntu'
        SERVER_PROD = 'ec2-34-213-109-81.us-west-2.compute.amazonaws.com'
    }
    stages {
        stage('Inicializando...') {
            steps {
                echo 'Asignando workspace y validando entorno.'
            }
        }
        stage('Entorno de desarrollo') {
            steps {
                sh 'docker compose up -d --build'
                //sh 'chmod +x script_jenkins.sh'
            }
        }
        stage('Analisis de codigo') {
            steps {
                sh 'docker exec cargas_academicas_app flake8 --max-complexity=10 --max-line-length=200 --ignore=F811,E402 .'
            }
        }
        stage('Pruebas unitarias') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    sleep time: 15, unit: 'SECONDS'
                    sh 'docker exec cargas_academicas_app python3 manage.py test'
                    sh """docker exec cargas_academicas_app bash -c "coverage run --branch --source='.' --omit=*test*,*migrations*,*__init*,*settings*,*apps*,*wsgi*,*admin.py,*asgi.py,manage.py,*urls.py manage.py test" """
                    sh 'docker exec cargas_academicas_app coverage html'
                    sh 'docker cp cargas_academicas_app:/app/htmlcov .'

                    publishHTML target:[
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: './htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Reporte de cobertura Cargas académicas',
                        reportTitles: 'Cobertura de código'
                    ]
                }
            }
        }

        stage('Pruebas de aceptacion') {
            steps {
                sh 'docker exec cargas_academicas_app python manage.py migrate'
                // sh 'docker exec cargas_academicas_app python manage.py shell < create_superuser.py'
                sh 'docker exec cargas_academicas_app python create_superuser.py'
                sh 'docker exec cargas_academicas_app bash -c "python manage.py runserver 0:8000 &"'
                sh 'docker exec -w /pruebas_aceptacion cargas_academicas_app behave features/login.feature'
            }
        }
        stage('Construir imagen producción') {
            steps {
                // sh 'cp /var/lib/jenkins/.env .'
                // sh 'cp /var/lib/jenkins/settings.py .'
                sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${VERSION} -f Dockerfile-prod ."
                sh "docker tag ${REGISTRY}/${IMAGE_NAME}:${VERSION} ${REGISTRY}/${IMAGE_NAME}:latest"
                // sh 'rm -rf .env settings.py'
            }
        }
        stage('Push de imagen a registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin ${REGISTRY}
                        docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}
                    """
                }
            }
        }
        stage('Desplegar en staging') {
            steps {
                sshagent(['prod-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${USER_PROD}@${SERVER_PROD} << 'EOF'
                        cd /home/ubuntu/cargas_academicas

                        # Respaldar el valor anterior de IMAGE_VERSION
                        if grep -q '^IMAGE_VERSION=' .env; then
                            OLD_VERSION=\$(grep '^IMAGE_VERSION=' .env | cut -d '=' -f2)
                            sed -i '/^IMAGE_VERSION_OLD=/d' .env
                            echo "IMAGE_VERSION_OLD=\$OLD_VERSION" >> .env
                        fi

                        # Actualizar o agregar IMAGE_VERSION con la nueva versión
                        sed -i '/^IMAGE_VERSION=/d' .env
                        echo "IMAGE_VERSION=${VERSION}" >> .env

                        # Confirmar contenido del archivo
                        echo "Contenido actualizado de .env:"
                        cat .env

                        # Desplegar con la nueva imagen
                        docker compose up -d
                        EOF
                    """
                }
            }

        }

    //     stage('Revisión por QA') {
    //         steps {
    //             input "Desplegar en producción?"
    //         }
    //     }
    //     stage('despliegue-pro') {
    //         steps {
    //             sh 'echo "Despliegue a producción"'
    //             sh 'echo "Despliegue a producción"'
    //         }
    //     }
    }
    post {
        always {
                sh 'docker compose down -v'
        }
        success {
            echo "Despliegue completado exitosamente con versión ${VERSION}"
        }
        failure {
            echo "El pipeline falló en algún paso."
        }
    }

}
