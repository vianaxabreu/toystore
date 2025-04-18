# ---- Stage 1: Build site with Jekyll ----
    FROM ruby:3.1-slim AS builder

    # Install dependencies
    RUN apt-get update && apt-get install -y build-essential nodejs git
    
    # Install Jekyll
    RUN gem install jekyll bundler
    
    WORKDIR /site
    COPY . .
    
    RUN bundle install && \
        bundle exec jekyll build -d /site/_site
    
    # ---- Stage 2: Serve with Nginx ----
    FROM nginx:alpine
    
    # Clean default site and copy built site
    RUN rm -rf /usr/share/nginx/html/*
    COPY --from=builder /site/_site /usr/share/nginx/html
    
    EXPOSE 80
    