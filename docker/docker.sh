case $1 in
	deploy)
		docker build . \
			-f docker/web/Dockerfile.prod \
			-t board.docker-registry.gewis.nl/wiso/web \
			&& docker push board.docker-registry.gewis.nl/wiso/web \
			&& docker build . \
			-f docker/nginx/Dockerfile.prod \
			-t board.docker-registry.gewis.nl/wiso/nginx \
			&& docker push board.docker-registry.gewis.nl/wiso/nginx
					;;
	up)
		docker build . \
			-f docker/web/Dockerfile.prod \
			-t board.docker-registry.gewis.nl/wiso/web \
			&& docker build . \
			-f docker/nginx/Dockerfile.prod \
			-t board.docker-registry.gewis.nl/wiso/nginx \
			&& docker-compose up -f docker-compose.prod.yml
					;;
	*)
		;;
esac
