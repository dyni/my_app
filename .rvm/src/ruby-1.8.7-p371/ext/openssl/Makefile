
SHELL = /bin/sh

#### Start of system configuration section. ####
top_srcdir = $(topdir)/.
srcdir = $(top_srcdir)/ext/openssl
topdir = ../..
hdrdir = $(top_srcdir)
VPATH = $(srcdir):$(topdir):$(hdrdir)
RUBYLIB = -
RUBYOPT = -rpurelib.rb
prefix = $(DESTDIR)/home/kostia/.rvm/rubies/ruby-1.8.7-p371
exec_prefix = $(prefix)
dvidir = $(docdir)
mandir = $(datarootdir)/man
datadir = $(datarootdir)
vendorarchdir = $(vendorlibdir)/$(sitearch)
sbindir = $(exec_prefix)/sbin
psdir = $(docdir)
oldincludedir = $(DESTDIR)/usr/include
libexecdir = $(exec_prefix)/libexec
sitedir = $(libdir)/ruby/site_ruby
pdfdir = $(docdir)
bindir = $(exec_prefix)/bin
archdir = $(rubylibdir)/$(arch)
sitelibdir = $(sitedir)/$(ruby_version)
localstatedir = $(prefix)/var
infodir = $(datarootdir)/info
localedir = $(datarootdir)/locale
htmldir = $(docdir)
vendorlibdir = $(vendordir)/$(ruby_version)
includedir = $(prefix)/include
datarootdir = $(prefix)/share
sharedstatedir = $(prefix)/com
sysconfdir = $(prefix)/etc
vendordir = $(libdir)/ruby/vendor_ruby
sitearchdir = $(sitelibdir)/$(sitearch)
docdir = $(datarootdir)/doc/$(PACKAGE)
rubylibdir = $(libdir)/ruby/$(ruby_version)
libdir = $(exec_prefix)/lib

CC = gcc
LIBRUBY = $(LIBRUBY_SO)
LIBRUBY_A = lib$(RUBY_SO_NAME)-static.a
LIBRUBYARG_SHARED = -Wl,-R -Wl,$(libdir) -L$(libdir) -l$(RUBY_SO_NAME)
LIBRUBYARG_STATIC = -l$(RUBY_SO_NAME)-static

RUBY_EXTCONF_H = 
CFLAGS   =  -fPIC -g -O2  -fPIC $(cflags) 
INCFLAGS = -I. -I../.. -I../../. -I../.././ext/openssl
DEFS     = 
CPPFLAGS = -DHAVE_ASSERT_H   
CXXFLAGS = $(CFLAGS) 
ldflags  = -L.  -rdynamic -Wl,-export-dynamic
dldflags = 
archflag = 
DLDFLAGS = $(ldflags) $(dldflags) $(archflag)
LDSHARED = $(CC) -shared
AR = ar
EXEEXT = 

RUBY_INSTALL_NAME = ruby
RUBY_SO_NAME = ruby
arch = x86_64-linux
sitearch = x86_64-linux
ruby_version = 1.8
ruby = $(topdir)/miniruby -I'$(topdir)' -I'$(top_srcdir)/lib' -I'$(extout)/$(arch)' -I'$(extout)/common' -I./- -I'$(top_srcdir)/ext' -rpurelib.rb
RUBY = $(ruby)
RM = rm -f
MAKEDIRS = mkdir -p
INSTALL = /usr/bin/install -c
INSTALL_PROG = $(INSTALL) -m 0755
INSTALL_DATA = $(INSTALL) -m 644
COPY = cp

#### End of system configuration section. ####

preload = 
CLEANFILES = mkmf.log
DISTCLEANFILES = 

all install static install-so install-rb: Makefile


clean:
		@-$(RM) $(CLEANLIBS) $(CLEANOBJS) $(CLEANFILES)

distclean:	clean
		@-$(RM) Makefile $(RUBY_EXTCONF_H) conftest.* mkmf.log
		@-$(RM) core ruby$(EXEEXT) *~ $(DISTCLEANFILES)

realclean:	distclean
