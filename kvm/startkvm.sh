#virsh shutdown base
#virsh snapshot-revert base base-1
#virsh start base

virsh destroy demo
virsh undefine demo


function flag() {
if  ping -c 1 10.110.25.62 >/dev/null 2>&1 ; then
        a="yes"
else   a="no"

fi
echo $a
}

ret=''

while [[ "$ret" != "yes" ]]; do
ret=`flag`
echo $ret
done
sleep 5
cd /home/test
java -jar jenkins-cli.jar -s http://10.110.18.40:8080/ connect-node 10.110.25.62 -f
sleep 10
