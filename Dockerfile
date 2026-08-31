dockerfile# Imagem base otimizada e com menos pacotes expostos
FROM python:3.9-slim

# Cria um grupo e um usuário comum sem privilégios administrativos
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Instala a biblioteca garantindo a versão mais recente e segura
RUN pip install --no-cache-dir flask==3.0.3

COPY app.py .

# Altera a propriedade dos arquivos para o usuário comum
RUN chown -R appuser:appgroup /app

# Altera o contexto de execução para o usuário comum (Bloqueia o Root!)
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
