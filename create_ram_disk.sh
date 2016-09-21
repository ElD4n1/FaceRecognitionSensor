echo "making RAM disk directory..."
mkdir -p /ram
echo "mounting RAM disk..."
mount -t tmpfs -o size=100m tmpfs /ram
echo "RAM disk created!"