# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provision :shell, path: "provision.sh"

  config.vm.box = "ubuntu/trusty64"

  config.vm.network :forwarded_port, guest: 80, host: 80, auto_correct:true
  config.vm.network :forwarded_port, guest: 443, host: 443, auto_correct:true
  config.vm.network :forwarded_port, guest: 8443, host: 8443, auto_correct:true
  config.vm.network :forwarded_port, guest: 8080, host: 8080, auto_correct:true
  config.vm.network :forwarded_port, guest: 3306, host: 3306, auto_correct:true
  config.vm.network :forwarded_port, guest: 27017, host: 27017, auto_correct:true  

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  config.vm.provider "virtualbox" do |vb|
     vb.customize ["modifyvm", :id, "--memory", "6000", "--cpus", "4"]
  end
end
