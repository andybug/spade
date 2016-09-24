package database

import log "github.com/Sirupsen/logrus"

type Sport struct {
	name string
	path string
}

func (s *Sport) ReadSport() {
	log.WithFields(log.Fields{
		"sport": s.name,
		"path": s.path,
	}).Info("database: reading sport")
}
