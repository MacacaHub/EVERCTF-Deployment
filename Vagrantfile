Vagrant.configure("2") do |config|
  config.vm.box = "debian/buster64"
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.define "devbox" do |devbox|
    devbox.vm.provider "libvirt" do |libvirt|
      libvirt.driver = "kvm"
      libvirt.cpus = "2"
      libvirt.memory = "2048"
    end
  end

  config.vm.define "prodbox", autostart: false do |prodbox|
    prodbox.vm.network "public_network",
      dev: "eno1",
      bridge: "eno1",
      mode: "bridge",
      ip: "140.117.169.216"
    prodbox.vm.provider "libvirt" do |libvirt|
      libvirt.driver = "kvm"
      libvirt.cpus = "4"
      libvirt.memory = "8192"
    end
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbooks/install-docker.yml"
  end
end