case $1 in
	deploy)
		sudo docker build . \
			-f docker/web/Dockerfile.prod \
			-t docker-registry.gewis.nl/wiso/web \
			&& sudo docker push docker-registry.gewis.nl/wiso/web \
			&& sudo docker build . \
			-f docker/nginx/Dockerfile.prod \
			-t docker-registry.gewis.nl/wiso/nginx \
			&& sudo docker push docker-registry.gewis.nl/wiso/nginx
					;;
	up)
		sudo docker build . \
			-f docker/web/Dockerfile.prod \
			-t docker-registry.gewis.nl/wiso/web \
			&& sudo docker build . \
			-f docker/nginx/Dockerfile.prod \
			-t docker-registry.gewis.nl/wiso/nginx \
			&& sudo docker-compose up -f docker-compose.prod.yml
					;;
	*)
		;;
esac
