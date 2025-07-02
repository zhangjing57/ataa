from oslo_config import cfg
# 读取config的信息
CONF = cfg.CONF

# 配置目录
CONF(args=[], default_config_files = ['/etc/dingo-command/auto_test.conf'])

# 默认数据
default_group = cfg.OptGroup(name='DEFAULT', title='default conf data')

default_opts = [
    cfg.StrOpt('loglevel', default="Debug", help='the level of log'),
    cfg.StrOpt('master_image_id', default="", help='the master image id'),
    cfg.StrOpt('master_flavor_id', default="", help='the master flavor id'),
    cfg.StrOpt('api_url', default="", help='the url of api request'),
    cfg.ListOpt('nameservers', default=[], help='the cluster router id'),
]

CONF.register_group(default_group)
CONF.register_opts(default_opts, default_group)

# redis数据
redis_group = cfg.OptGroup(name='redis', title='redis conf data')
redis_opts = [
    cfg.StrOpt('redis_ip', default=None, help='the redis ip'),
    cfg.IntOpt('redis_port', default=None, help='the redis port'),
    cfg.StrOpt('redis_password', default=None, help='the redis password'),
    cfg.StrOpt('sentinel_url', default=None, help='the redis sentinel'),
]

# 注册redis配置
CONF.register_group(redis_group)
CONF.register_opts(redis_opts, redis_group)

# ironic的配置信息
ironic_group = cfg.OptGroup(name='ironic', title='ironic conf data')
ironic_opts = [
    cfg.StrOpt( 'auth_url', default='http://10.220.56.254:5000', help='auth url'),
    cfg.StrOpt( 'auth_type', default="password", help='auth type'),
    cfg.StrOpt( 'project_domain', default="default", help='project domain'),
    cfg.StrOpt( 'user_domain', default='default', help='user domain'),
    cfg.StrOpt( 'project_name', default='service', help='project name'),
    cfg.StrOpt( 'user_name', default='ironic', help='user name'),
    cfg.StrOpt( 'password', default='dKF6StAnNfzTQjXVX3MIGWSRi0JagLxAKZDK6zLk', help='password'),
    cfg.StrOpt( 'region_name', default='RegionOne', help='region name'),
]
# 注册ironic配置
CONF.register_group(ironic_group)
CONF.register_opts(ironic_opts, ironic_group)

# nova的配置信息
nova_group = cfg.OptGroup(name='nova', title='nova conf data')
nova_opts = [
    cfg.StrOpt( 'auth_url', default='http://10.220.56.254:5000', help='auth url'),
    cfg.StrOpt( 'auth_type', default="password", help='auth type'),
    cfg.StrOpt( 'project_domain', default="default", help='project domain'),
    cfg.StrOpt( 'user_domain', default='default', help='user domain'),
    cfg.StrOpt( 'project_name', default='service', help='project name'),
    cfg.StrOpt( 'user_name', default='nova', help='user name'),
    cfg.StrOpt( 'password', default='XModTf5fcvUw7aAr3CUBBVdO38WQS15QQwNqVjGJ', help='password'),
    cfg.StrOpt( 'region_name', default='RegionOne', help='region name'),
]
# 注册nova配置
CONF.register_group(nova_group)
CONF.register_opts(nova_opts, nova_group)

# cloudkitty的配置信息
cloudkitty_group = cfg.OptGroup(name='cloudkitty', title='cloudkitty conf data')
cloudkitty_opts = [
    cfg.StrOpt( 'auth_url', default='http://10.220.58.246:5000', help='auth url'),
    cfg.StrOpt( 'auth_type', default="password", help='auth type'),
    cfg.StrOpt( 'project_domain', default="default", help='project domain'),
    cfg.StrOpt( 'user_domain', default='default', help='user domain'),
    cfg.StrOpt( 'project_name', default='service', help='project name'),
    cfg.StrOpt( 'user_name', default='cloudkitty', help='user name'),
    cfg.StrOpt( 'password', default='LRnxEqGtZqtBC2zmwDwg9510x1sGnMPB4eOOQa0w', help='password'),
    cfg.StrOpt( 'region_name', default='RegionOne', help='region name'),
]
# 注册cloudkitty配置
CONF.register_group(cloudkitty_group)
CONF.register_opts(cloudkitty_opts, cloudkitty_group)

# nova的配置信息
cinder_group = cfg.OptGroup(name='cinder', title='cinder conf data')
cinder_opts = [
    cfg.StrOpt( 'auth_url', default='http://10.220.56.254:5000', help='auth url'),
    cfg.StrOpt( 'auth_type', default="password", help='auth type'),
    cfg.StrOpt( 'project_domain', default="default", help='project domain'),
    cfg.StrOpt( 'user_domain', default='default', help='user domain'),
    cfg.StrOpt( 'project_name', default='service', help='project name'),
    cfg.StrOpt( 'user_name', default='nova', help='user name'),
    cfg.StrOpt( 'password', default='XModTf5fcvUw7aAr3CUBBVdO38WQS15QQwNqVjGJ', help='password'),
    cfg.StrOpt( 'region_name', default='RegionOne', help='region name'),
]
# 注册nova配置
CONF.register_group(cinder_group)
CONF.register_opts(cinder_opts, cinder_group)

# 数据库
database_group = cfg.OptGroup(name='database', title='database')
database_opts = [
    cfg.StrOpt('connection', default='mysql+pymysql://root:HworLIIDvmTRsPfQauNskuJF8PcoTuULfu3dEHFg@10.220.'
                                     '56.254:3306/dingoops?charset=utf8mb3', help='the mysql url'),
]
# 注册mysql数据库
CONF.register_group(database_group)
CONF.register_opts(database_opts, database_group)